import tilelang
import tilelang.language as T

# 声明动态符号
M = T.dynamic("M")
N = T.dynamic("N")
K = T.dynamic("K")

@tilelang.jit(out_idx=[-1])
def matmul(block_M, block_N, block_K, dtype=T.float16, accum_dtype=T.float32):
#def matmul(M, N, K, block_M, block_N, block_K, dtype=T.float16, accum_dtype=T.float32):
    @T.prim_func
    def gemm(
        A: T.Tensor((M, K), dtype),
        B: T.Tensor((K, N), dtype),
        C: T.Tensor((M, N), dtype),
    ):
        with T.Kernel(T.ceildiv(N, block_N), T.ceildiv(M, block_M), threads=128) as (bx, by):
            A_shared = T.alloc_shared((block_M, block_K), dtype)
            B_shared = T.alloc_shared((block_K, block_N), dtype)
            C_local = T.alloc_fragment((block_M, block_N), accum_dtype)

            T.clear(C_local)
            for k in T.Pipelined(T.ceildiv(K, block_K), num_stages=3):
                T.copy(A[by * block_M, k * block_K], A_shared)
                T.copy(B[k * block_K, bx * block_N], B_shared)
                T.gemm(A_shared, B_shared, C_local)

            T.copy(C_local, C[by * block_M, bx * block_N])

    return gemm

def main():
    kernel = matmul(128, 128, 32, dtype=T.float16)

    import torch

    a = torch.randn(1024, 1024, dtype=torch.float16).cuda() #.half()
    b = torch.randn(1024, 1024, dtype=torch.float16).cuda() #.half()

    c = kernel(a, b)
    print(a.shape, a.dtype, a.is_contiguous(), b.shape, b.dtype, b.is_contiguous())
    print("is_bf16_supported=", torch.cuda.is_bf16_supported())
    ref_c = a.cpu().float() @ b.cpu().float()
    ref_c = ref_c.cuda().to(torch.float16)

    print("c:")
    print(c)
    print("ref_c:")
    print(ref_c)

    torch.testing.assert_close(c, ref_c, rtol=1e-1, atol=0.05)
    print("All check passed.")

    # Get CUDA Source
    print("CUDA Source:")
    print(kernel.get_kernel_source())

    # benchmark
    #profiler = kernel.get_profiler()
    #latency = profiler.do_bench(backend="cupti")
    # latency = profiler.do_bench()
    #print(f"tilelang Latency: {latency}ms")


def run_regression_perf():
    kernel = matmul(1024, 1024, 1024, 128, 128, 32, dtype=T.float32)
    profiler = kernel.get_profiler()
    return profiler.do_bench(backend="cupti")


if __name__ == "__main__":
    main()

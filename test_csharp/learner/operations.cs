using System;

namespace cs_learner{

    public class OperationLearner {

        public string name = "operations";
        
        public void print() {
            int m = 10, n = 5;
            Console.WriteLine("m+n={0}", m + n);
            Console.WriteLine("m-n={0}", m - n);
            Console.WriteLine("m*n={0}", m * n);
            Console.WriteLine("m/n={0}", m / n);
            Console.WriteLine("m%n={0}", m % n);
            Console.WriteLine("m++={0}", m++);
            Console.WriteLine("m--={0}", m--);
            Console.WriteLine("++m={0}", ++m);
            Console.WriteLine("--m={0}", --m);
            m += 2;
            Console.WriteLine("m+=2:m={0}", m);
            m -= 2;
            Console.WriteLine("m-=2:m={0}", m);
            // *=
            // /=
            // %=

            m <<= 1;
            Console.WriteLine("m<<=1:m={0}", m);
            m >>= 1;
            Console.WriteLine("m>>=1:m={0}", m);

            // ^=
            // &=
            // |=

            Console.WriteLine("sizeof(int)={0}", sizeof(int));
            Console.WriteLine("typeof(int)={0}", typeof(int));
            Console.WriteLine("false?m:n={0}", false ? m : n);
            Console.WriteLine("true?m:n={0}", true ? m : n);
            Console.WriteLine("m is int:{0}", m is int);

            // as 强制类型转换

        }

        public static void test(OperationLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }

    };
}
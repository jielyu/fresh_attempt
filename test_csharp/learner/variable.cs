using System;

namespace cs_learner{
    
    public class VariableLearner{
        public bool b_var = true;
        public byte by_var = Byte.MaxValue;
        public sbyte sb_var = SByte.MaxValue;
        public char c_var = Char.MaxValue;
        public short sh_var = short.MaxValue;
        public ushort us_var = ushort.MaxValue;
        public int i_var = int.MaxValue;
        public uint ui_var = uint.MaxValue;
        public long l_var = long.MaxValue;
        public ulong ul_var = ulong.MaxValue;
        public decimal d_var = decimal.MaxValue;
        public float f_var = float.MaxValue;
        public double db_var = double.MaxValue;
        
        
        public string name = "variable";

        public void print() {
            // 测试基本数据类型，在编译时决定数据类型
            Console.WriteLine("bool:" + b_var);
            Console.WriteLine("byte:" + by_var);
            Console.WriteLine("sbyte:" +sb_var);
            Console.WriteLine("char:" + (int)c_var);
            Console.WriteLine("short:" + sh_var);
            Console.WriteLine("ushort:" + us_var);
            Console.WriteLine("int:" + i_var);
            Console.WriteLine("uint:" + ui_var);
            Console.WriteLine("long:" +l_var);
            Console.WriteLine("decimal:" + d_var);
            Console.WriteLine("float:" + f_var);
            Console.WriteLine("double:" + db_var);
            // 测试动态数据类型，在运行时决定数据类型
            dynamic d1_test = 12;
            dynamic d2_test = false;
            Console.WriteLine("dynamic:d1=" + d1_test);
            Console.WriteLine("dynamic:d2=" + d2_test);
            d1_test = "hello";
            Console.WriteLine("dynamic:d1=" + d1_test);

            unsafe{
                int a = 123;
                int * ptr_ivar = & a;
                *ptr_ivar = 1024;
                Console.WriteLine("*ptr_ivar:" + (*ptr_ivar));
            }
        }
        
        public static void test(VariableLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
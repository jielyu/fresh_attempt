using System;

namespace cs_learner{
    public class LoopLearner {

        private string name = "loop";

        public void print() {
            
            Console.Write("for_loop:");
            for (int i = 0; i < 10; ++i) {
                Console.Write(i + ",");
            }
            Console.WriteLine();

            Console.Write("while_loop:");
            int j = 0;
            while (j < 10) {
                Console.Write(j + ",");
                ++j;
            }
            Console.WriteLine();

            Console.Write("for_each:");
            int[] arr = new int[]{0,1,2,3,4,5,6,7,8,9};
            foreach(int elem in arr) {
                Console.Write(elem + ",");
            }
            Console.WriteLine();
        }

        public static void test(LoopLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");

        }
    };
}
using System;

namespace cs_learner{

    public class ConditionLearner{
        public string name = "condition";
        public void print() {
            // 测试if条件语句
            int m = 12;
            if (m is int) {
                Console.WriteLine("run true switch");
            } else {
                Console.WriteLine("run else switch");
            }

            // 测试switch语句
            int n = 0;
            switch(n) {
                case 0: Console.WriteLine("case 0");break;
                case 1: Console.WriteLine("case 1");break;
                default: Console.WriteLine("default case");break;
            }
        }

        public static void test(ConditionLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
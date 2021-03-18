using System;

namespace cs_learner{

    delegate void LambdaFunc();
    public class LambdaLearner{
        public string name = "lambda";

        public void print() {
            LambdaFunc func = delegate() {
                Console.WriteLine("run lambda func");
            };
            func();
        }

        public static void test(LambdaLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
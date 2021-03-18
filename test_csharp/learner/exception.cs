using System;

namespace cs_learner {

    class ExceptionLearner {
        public string name = "exception";

        public void print() {
            try{
                int div = 0;
                int a = 10 / div;
            } catch (Exception e) {
                Console.WriteLine(e);
            } finally {
                Console.WriteLine("finally");
            }
        }

        public static void test(ExceptionLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
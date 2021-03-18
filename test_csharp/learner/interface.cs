using System;

namespace cs_learner{
    public interface IAclass {
        public void print();
    }

    public interface IBclass {
        public void show();
    }

    public class Impl : IAclass, IBclass {
        public void print() {
            Console.WriteLine("Impl IAclass");
        }
        public void show() {
            Console.WriteLine("Impl IBclass");
        }
    }

    public class InterfaceLearner {
        public string name = "interface";

        public void print() {
            Impl impl = new Impl();
            impl.print();
            impl.show();
        }

        public static void test(InterfaceLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    }
}
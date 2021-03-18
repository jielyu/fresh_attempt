using System;

namespace cs_learner{

    public class A{
        public virtual void print() {
            Console.WriteLine("class A");
        }
    };

    public class B : A {
        public override void print() {
            Console.WriteLine("class B");
        }
    };

    public class PolyMorphicLearner{
        public string name = "poly_morphic";

        public void print() {
            A a = new A();
            a.print();
            a = new B();
            a.print();
        }

        public static void test(PolyMorphicLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
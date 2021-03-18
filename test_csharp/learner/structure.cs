using System;

namespace cs_learner{
    public struct AStruct {
        public string name;

        public AStruct(string name) {
            //this.setValues(name);
            this.name = name;
        }

        public void setValues(string name) {
            this.name = name;
        }

        public void print() {
            Console.WriteLine("name={0}", this.name);
        }
    };

    public class StructLearner {
        public AStruct aStruct;
        public string name = "struct";
        
        public void print() {
            this.aStruct = new AStruct("init");
            this.aStruct.print();
            this.aStruct.setValues("helloStruct");
            this.aStruct.print();
        }

        public static void test(StructLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
using System;
using System.IO;

namespace cs_learner{
    public class FileLearner{
        public string name = "file";

        public void print() {
            StreamReader fs = new StreamReader("./learner/file.cs");
            string line;
            while (null != (line = fs.ReadLine())) {
                Console.WriteLine(line);
            }
        }

        public static void test(FileLearner obj) {
            Console.WriteLine(obj.name + ":begin to run testcase.");
            obj.print();
            Console.WriteLine(obj.name + ":end.");
        }
    };
}
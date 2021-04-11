using System;

namespace cs_learner{

/*当前类用于测试基本的C#语法
*/
public class BasicLearner {
    public int rows{get;set;}  // 行数
    public int cols{get;set;}  // 列数
    public string name{get{return "basic";}} // 当前对象的名嘴标号

    public void print() {
        Console.WriteLine("Hello {0}, Hello {1}", "World", "C#");
    }

    /* 用于测试
    */
    public static void test(BasicLearner obj) {
        Console.WriteLine(obj.name + ":begin to run testcase for basic grammar.");
        obj.rows = 1920;
        obj.cols = 1080;
        obj.print();
        Console.WriteLine(obj.name + ":end.");
    }

};
}
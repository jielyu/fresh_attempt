using System;

namespace cs_learner
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World! Hello C#");
            // basic grammar case
            BasicLearner basic_learner = new BasicLearner();
            BasicLearner.test(basic_learner);
            // variable grammar case
            VariableLearner var_learner = new VariableLearner();
            VariableLearner.test(var_learner);
            // operation cases
            OperationLearner op_learner = new OperationLearner();
            OperationLearner.test(op_learner);
            // condition cases
            ConditionLearner cond_learner = new ConditionLearner();
            ConditionLearner.test(cond_learner);
            // lopp case
            LoopLearner loop_learner = new LoopLearner();
            LoopLearner.test(loop_learner);
            // struct case
            StructLearner struct_learner = new StructLearner();
            StructLearner.test(struct_learner);
            // poly morphic learner
            PolyMorphicLearner pm_learner = new PolyMorphicLearner();
            PolyMorphicLearner.test(pm_learner);
            // interface case
            InterfaceLearner interface_learner = new InterfaceLearner();
            InterfaceLearner.test(interface_learner);
            // exception case
            ExceptionLearner ex_learner = new ExceptionLearner();
            ExceptionLearner.test(ex_learner);
            // file case
            FileLearner file_learner = new FileLearner();
            FileLearner.test(file_learner);
            // lambda case
            LambdaLearner lambda_learner = new LambdaLearner();
            LambdaLearner.test(lambda_learner);
        }
    }
}

import 'dart:io';

import 'package:args/args.dart';
import 'package:args/command_runner.dart';

class TestCommand extends Command {

    final name = "test";
    final description = "test command";

    TestCommand() {
        this.argParser.addOption('opt', abbr: 'o', defaultsTo: 'hello', allowed: ['hello', 'world']);
        this.argParser.addMultiOption('mul', abbr: 'm', help: 'help info');
        this.argParser.addFlag('all', abbr: 'a', help: 'help info');
    }

    void run() {
        print(this.argResults?['opt']);
        print(this.argResults?['mul']);
        print(this.argResults?['all']);
    }
}

int main(List<String> args) {

    // CommandRunner, with help automatically
    print('test for CommandRunner:');
    var runner = CommandRunner('args', '');
    runner.addCommand(TestCommand());
    runner.run(args).catchError((err){
        if (err is! UsageException) throw err;
        print('UsageException: $err');
        exit(64);
    });

    // ArgParser, not allow help otherwise crash 
    print('test for ArgParser:');
    var parser = ArgParser();
    parser.addCommand('test');
    parser.addFlag('help', abbr: 'h');
    parser.addOption('opt', abbr: 'o', defaultsTo: 'hello', allowed: ['hello', 'world']);
    parser.addMultiOption('mul', abbr: 'm', help: 'test multiple options');
    parser.addFlag('all', abbr: 'a');
    var results = parser.parse(args);
    if (results['help']) {
        print(parser.usage);
        return 0;
    }
    print("opt: ${results['opt']}");
    print("mul: ${results['mul']}");
    print("all: ${results['all']}");
    return 0;
}
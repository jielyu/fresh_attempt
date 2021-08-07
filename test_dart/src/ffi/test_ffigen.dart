import 'dart:io' show Platform, Directory;
import 'dart:ffi' as ffi;
import 'package:path/path.dart' as path;
import 'hello_ffi.dart';

int main() {
  // Open the dynamic library
  var libraryPath =
      path.join(Directory.current.path, 'hello_library', 'libhello.so');
  if (Platform.isMacOS) {
    libraryPath = path.join(
        Directory.current.path, 'hello_library/build', 'libhello.dylib');
  }
  if (Platform.isWindows) {
    libraryPath = path.join(
        Directory.current.path, 'hello_library', 'build/Release', 'hello.dll');
  }

  final dylib = ffi.DynamicLibrary.open(libraryPath);

  var nl = new NativeLibrary(dylib);
  nl.hello_world();
  return 0;
}

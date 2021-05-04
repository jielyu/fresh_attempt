void main(List<String> args) {
  try {
    throw Exception("test");
  } catch (e) {
    print(e);
  } finally {
    print("end");
  }
}

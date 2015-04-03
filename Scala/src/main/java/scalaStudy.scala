object scalaStudy {

  val print = (str:String) => {println(str);}

  def main(args:Array[String]){
    print("helloWorld");
    printHello({print("名前渡し");"helloWorld"});
  }

  def printHello(str: => String){
    print(str);
  }
}
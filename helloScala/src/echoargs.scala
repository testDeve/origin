object echoargs {
  def main(args:Array[String]){
    args.foreach {args => println(args)}
    args.foreach(println);
  }
}
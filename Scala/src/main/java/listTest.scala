package testScala

import scala.collection.mutable.ListBuffer;

object listTest {

  var list = ListBuffer[String]("帰りたい","帰りたい")

  def main(str:Array[String]){
    list += "あったかホームが待っている";
    list.foreach(println);
  }
}
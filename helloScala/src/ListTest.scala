object ListTest {
  def main(args:Array[String]){
    val oneTwo = List(1,2);
    val threeFour = List(3,4);
    val oneTwoThreeFour = oneTwo:::threeFour;
    
    oneTwoThreeFour.foreach(println);
    println(oneTwoThreeFour.count { num => num > 2 })
    println(oneTwoThreeFour.filter { num => num < 3 })
  }
}
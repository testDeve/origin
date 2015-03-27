import java.util.HashMap

object MapTest {
  def main(args:Array[String]){
    var capital = Map("US"->"Washington","France"->"Paris");
    capital += ("Japan"->"Tokyo")
    println(capital("France"))
  }
}
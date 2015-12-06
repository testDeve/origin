class User
  
  @@count = 0
  
  def initialize(name)
    @name = name
    @@count += 1
  end
  
  def sayHi
    puts "count #{@@count} hello, my name is #{@name}"
  end
  
  def User.say
    puts "Hello User.Class"
  end
end
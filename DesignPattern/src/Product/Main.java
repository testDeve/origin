package Product;

public class Main {
    public static void main(String[] args){
    	Manager manager = new Manager();
    	UnderlinePen upen = new UnderlinePen('~');
    	MessageBox mbox = new MessageBox('*');
    	MessageBox sbox = new MessageBox('/');
    	manager.register("strong message", upen);
    	manager.register("warning box", mbox);
    	manager.register("slash box", sbox);
    	
    	//生成
    	Product p1 = manager.create("strong message");
    	p1.use("Hello, World");
    	p1 = manager.create("warning box");
    	p1.use("Hello, World");
    	p1 = manager.create("slash box");
    	p1.use("Hello, World");
    }
}

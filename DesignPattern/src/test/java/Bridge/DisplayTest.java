package Bridge;

import junit.framework.TestCase;

public class DisplayTest extends TestCase {
	
	public void testDisplay(){
		Display dp = new Display(new StringDisplayImpl("UnitTest"));
	}
	
	public void testOpen(){
		Display dp = new Display(new StringDisplayImpl("UnitTest"));
		dp.open();
	}
	
	public void testPrint(){
		Display dp = new Display(new StringDisplayImpl("UnitTest"));
		dp.print();
	}
	
	public void testClose(){
		Display dp = new Display(new StringDisplayImpl("UnitTest"));
		dp.close();
	}
	
	public void testDispaly(){
		Display dp = new Display(new StringDisplayImpl("UnitTest"));
		dp.display();
	}

}

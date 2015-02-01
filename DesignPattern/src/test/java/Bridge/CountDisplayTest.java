package Bridge;

import junit.framework.TestCase;

public class CountDisplayTest extends TestCase {
	
	public void testCountDisplay(){
		CountDisplay cd = new CountDisplay(new StringDisplayImpl("UnitTest"));
	}
	
	public void testMultiDisplay(){
		CountDisplay cd = new CountDisplay(new StringDisplayImpl("UnitTest"));
		cd.multiDisplay(5);
	}

}

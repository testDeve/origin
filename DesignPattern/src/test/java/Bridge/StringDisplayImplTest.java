package Bridge;

import junit.framework.TestCase;

public class StringDisplayImplTest extends TestCase {
	
	public void testStringDisplayImpl(){
		StringDisplayImpl impl = new StringDisplayImpl("UnitTest");
	}
	
	public void testRawOpen(){
		StringDisplayImpl impl = new StringDisplayImpl("UnitTest");
		impl.rawOpen();
	}
	
	public void testRawPrint(){
		StringDisplayImpl impl = new StringDisplayImpl("UnitTest");
		impl.rawPrint();
	}
	
	public void testRawClose(){
		StringDisplayImpl impl = new StringDisplayImpl("UnitTest");
		impl.rawClose();
	}
}

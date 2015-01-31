package Adapter;

import junit.framework.TestCase;

public class BannerTest extends TestCase{
    
    public void testBanner(){
         Banner banner = new Banner("Banner");   
	}
    
    public void testShowWithParen(){
         Banner banner = new Banner("Banner");
         banner.showWithParen();
	}
    
    public void testShowWithAster(){
        Banner banner = new Banner("Banner");
        banner.showWithAster();
   }
}

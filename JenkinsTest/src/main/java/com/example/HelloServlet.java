package com.example;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class HelloServlet extends HttpServlet {
    
  public void doGet (HttpServletRequest req, HttpServletResponse res)
    throws ServletException, IOException {
        
    PrintWriter out = res.getWriter();
    out.println("<html><body>");
    out.println("<h1>Hello Servlet !!</h1>");
    out.println("</body></html>");
  }
}
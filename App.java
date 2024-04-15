import java.sql.*;

public class App {
   static final String DB_URL = "jdbc:mysql://localhost:3306/subash";
   static final String USER = "root";
   static final String PASS = "cnp200@HW";
   static final String QUERY = "SELECT * FROM students";

   public static void main(String[] args) {
      // Open a connection
      try(Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
         Statement stmt = conn.createStatement();
         ResultSet rs = stmt.executeQuery(QUERY);) {
         // Extract data from result set
         while (rs.next()) {
            // Retrieve by column name
            System.out.print("Student_ID: " + rs.getString("Student_ID"));
            System.out.print(", Name: " + rs.getString("Name"));
            System.out.println(", AGE: " + rs.getFloat("AGE"));
         }
      } catch (SQLException e) {
         e.printStackTrace();
      } 
   }
}
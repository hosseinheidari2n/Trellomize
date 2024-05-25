using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace ApProject2
{
    class Program
    {
        static void Main(string[] args)
        {

            FirstCommandList();

            Console.ReadKey();
        }
        public static void FirstCommandList()
        {
            Console.WriteLine("Hello , Wellcome to our Project Managment.");
            Console.WriteLine("1.Create Manager");
            Console.WriteLine("2.Login as Manager");
            Console.WriteLine("3.Sign In as Client");
            Console.WriteLine("4.Login as Client");
            Console.WriteLine("Please enter a number bitween 1 to 4...");
            string n = Console.ReadLine();
            if (n == "1")
            {
                CreateManager();
            }
            else if (n == "2")
            {
                LoginManager();
            }
            else if (n == "3")
            {
                CreateClient();
            }
            else if (n == "4")
            {
                LoginClient();
            }
            else
            {
                Console.WriteLine("Please enter a number bitween 1 to 4...");
                FirstCommandList();
            }
        }
        public static void CreateManager() // ok
        {
            string filePath = "manager.txt";

            if (File.Exists(filePath))
            {
                Console.WriteLine("Manager has been Created!");
                Console.WriteLine("Press any key...");
                Console.ReadLine();
                FirstCommandList();
            }
            else
            {
                Console.WriteLine("Please enter your userName...");
                string userName = Console.ReadLine();
                Console.WriteLine("Please enter your password...");
                string password1 = Console.ReadLine();
                string password = HashPassword(password1);
                Manager manager = new Manager(userName, password);

                string content = $"{manager.UserName} : {manager.Password}\n";

                File.AppendAllText("manager.txt", content);

                Console.WriteLine("Saved in manager.txt");
                Console.WriteLine("Press any enter...");
                Console.ReadLine();
                FirstCommandList();
            }
        }
        static void LoginManager() // ok
        {
            string filePath = "manager.txt";

            if (File.Exists(filePath))
            {
                Console.WriteLine("Please enter your userName...");
                string userName = Console.ReadLine();
                Console.WriteLine("Please enter your password...");
                string password1 = Console.ReadLine();
                string password = CalculateHash(password1);

                string[] lines = File.ReadAllLines(filePath);
                foreach (var line in lines)
                {
                    string[] parts = line.Split(':');
                    if (parts.Length == 2)
                    {
                        string storedUsername = parts[0].Trim();
                        string storedPasswordHash = parts[1].Trim();

                        if (storedUsername == userName && storedPasswordHash == password)
                        {
                            SecondCommandList();
                        }
                        else
                        {
                            Console.WriteLine("UserName or Password is not correct");
                            LoginManager();
                        }
                    }
                }
            }
            else
            {
                Console.WriteLine("First Create Manager!");
            }
        }
        static void CreateClient()
        {
            Console.WriteLine("Please enter your userName...");
            string inputUsername = Console.ReadLine();
            Console.WriteLine("Please enter your password...");
            string password1 = Console.ReadLine();
            string inputPassword = HashPassword(password1);

            string filePath = "client.txt";

            if (File.Exists(filePath))
            {
                string[] lines = File.ReadAllLines(filePath);

                bool found = false;

                foreach (string line in lines)
                {
                    string[] part = line.Split(':');
                    if (part.Length == 2 && part[0].Trim() == inputUsername)
                    {
                        found = true;
                        break;
                    }
                }

                if (!found)
                {
                    // نام کاربری یافت نشد، بنابراین اضافه کنید
                    Client client = new Client(inputUsername, inputPassword);

                    string content = $"{client.UserName} : {client.Password}\n";

                    File.AppendAllText("client.txt", content);

                    Console.WriteLine("Saved in client.txt");
                }
                else
                {
                    // نام کاربری قبلاً وجود داشت
                    Console.WriteLine("This userName exists. Please enter another userName.");
                    CreateClient(); // دوباره ورود به تابع برای دریافت نام کاربری جدید
                }

                Console.WriteLine("Press any enter...");
                Console.ReadLine();
                FirstCommandList();
            }
            else
            {
                Client client = new Client(inputUsername, inputPassword);
                string content = $"{client.UserName} : {client.Password}\n";
                File.AppendAllText("client.txt", content);
                Console.WriteLine("Saved in client.txt");
                Console.WriteLine("Press any enter...");
                Console.ReadLine();
                FirstCommandList();

            }
            
        } // ok
        static void LoginClient() // ok
        {
            // مسیر فایل مورد نظر
            string filePath = "client.txt";

            // ایجاد یک دیکشنری برای نگهداری اطلاعات کاربران (نام کاربری و رمز عبور)
            Dictionary<string, string> users = new Dictionary<string, string>();

            // خواندن محتوای فایل و جداسازی نام کاربری و رمز عبور
            try
            {
                using (StreamReader sr = new StreamReader(filePath))
                {
                    string line;
                    while ((line = sr.ReadLine()) != null)
                    {
                        string[] parts = line.Split(':');
                        if (parts.Length == 2)
                        {
                            string username = parts[0].Trim();
                            string password = parts[1].Trim();
                            users[username] = password;
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine("خطا: " + e.Message);
            }

            // اعتبارسنجی کاربر
            Console.WriteLine("Please enter your userName...");
            string inputUsername = Console.ReadLine();
            Console.WriteLine("Please enter your password...");
            string inputPassword = Console.ReadLine();

            // بررسی وجود کاربر در دیکشنری و مطابقت رمز عبور
            if (users.ContainsKey(inputUsername) && users[inputUsername] == CalculateHash(inputPassword))
            {
                SecondCommandList();
            }
            else
            {
                Console.WriteLine("UserName or Password is not correct");
                LoginClient();
            }
        }
        static string HashPassword(string password)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] passwordBytes = Encoding.UTF8.GetBytes(password);
                byte[] hashBytes = sha256.ComputeHash(passwordBytes);
                return BitConverter.ToString(hashBytes).Replace("-", "").ToLower();
            }
        } // ok
        static string CalculateHash(string input)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(input));
                StringBuilder builder = new StringBuilder();
                for (int i = 0; i < bytes.Length; i++)
                {
                    builder.Append(bytes[i].ToString("x2"));
                }
                return builder.ToString();
            }
        } // ok

        //-----------------------------------------------------------
        static void SecondCommandList()
        {
            Console.WriteLine("1.Create Project");
            Console.WriteLine("2.Show Projects");
        }

        static void CreateProject(Client leader)
        {
            Console.WriteLine("Enter an Id for Project");
            string id = Console.ReadLine();
            Console.WriteLine("Enter name of Project");
        }
    }
}

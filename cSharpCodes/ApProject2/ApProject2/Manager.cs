using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ApProject2
{
    class Manager
    {
        public string UserName { get; set; }
        public string Password { get; set; }

        public Manager(string userName, string password)
        {
            this.UserName = userName;
            this.Password = password;
        }
    }
}

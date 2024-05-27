using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ApProject2
{
    class Client
    {
        public string UserName { get; set; }
        public string Password { get; set; }
        public bool Validate { get; set; }

        public Client(string userName, string password)
        {
            this.UserName = userName;
            this.Password = password;
        }
    }
}

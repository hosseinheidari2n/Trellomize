using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ApProject2
{
    class Project
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public List<Client> Members { get; set; }
        public List<Task> Tasks { get; set; }
        public string Leader { get; set; }

        public Project()
        {
            Id = Guid.NewGuid().ToString(); // تولید شناسه منحصر به فرد
            Members = new List<Client>();
            Tasks = new List<Task>();
        }
    }
}

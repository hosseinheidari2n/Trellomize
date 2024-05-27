using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ApProject2
{
    class Task
    {
        public string Id { get; private set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public List<string> Assignees { get; set; }
        public Priority Priority { get; set; }
        public Status Status { get; set; }
        public List<string> History { get; set; }
        public List<string> Comments { get; set; }

        public Task()
        {
            Id = Guid.NewGuid().ToString(); // تولید شناسه منحصر به فرد
            StartDate = DateTime.Now;
            EndDate = DateTime.Now.AddHours(24);
            Assignees = new List<string>();
            Priority = Priority.Low; // مقدار پیشفرض برای اولویت
            Status = Status.Backlog; // مقدار پیشفرض برای وضعیت
            History = new List<string>();
            Comments = new List<string>();
        }
    }
}

import frappe
from frappe import _

def get_assigned_user(doctype_name, doctype_id):
    assigned_users = frappe.get_all(
			"ToDo",
			fields=["allocated_to"],
			filters={
				"reference_type": doctype_name,
				"reference_name": doctype_id,
				"status": ("!=", "Cancelled"),
			},
			pluck="allocated_to",
		)
    users = set(assigned_users)
    return users
  
@frappe.whitelist()
def get_ongoing_projects():
    html = ''
    html += '''
        <style>
        .widget.number-widget-box{min-height:300px;} 
        .widget.number-widget-box .widget-body .widget-content .number{font-size:14px;font-weight:400;max-width:100%}         
        .progress-group{width:260px;padding:5px;}
        .progress-group:hover{background-color:#d3d3d3}
        .widget.number-widget-box .widget-body .widget-content .number .progress-group.active {background-color:#d3d3d3}
        </style>
    '''
    
    progress_css = [
        'bg-primary',
        'bg-secondary',
        'bg-success',
        'bg-info',
        'bg-warning',
        'bg-danger',
        'bg-light',
        'bg-dark',
        'bg-white',
        'bg-transparent'
    ]
#     <div class="progress-group">
# Add Products to Cart
# <span class="float-right"><b>160</b>/200</span>
# <div class="progress progress-sm">
# <div class="progress-bar bg-primary" style="width: 80%;"></div>
# </div>
# </div>
    # html += '<div class="col-md-4">'
    projects_list = frappe.db.get_list('Project', 
        filters={
            'status':'Open'
        },
        fields=['name','project_name']        
    )
    if not projects_list:
        frappe.throw(_("On Going Projects not found."))
    else:
        i=0
        for row in projects_list:
            html += '<div class="progress-group" onclick="get_project_contracts(\''+row.name+'\', this)">'+row.project_name
            tasks_data = frappe.db.get_list('Task',
                filters = {
                    'project':row.name
                },
                fields=['count(name) as count', 'status'],
                group_by='status'
            )
            total_task_count = 0
            completed_tasks = 0
            if tasks_data:
                for tasks in tasks_data:
                    if tasks.status and tasks.status == 'Completed':
                        completed_tasks = tasks.count
                    total_task_count += tasks.count
                    
                # html += '<div class="task-count">'
                # html += '</span>&nbsp;&nbsp;<span id="remaining-tasks" style="float:right">'+str(completed_tasks)+'/'+str(total_task_count)+'</span>'
            html += f'<span class="float-right"><b>{str(completed_tasks)}</b>/{str(total_task_count)}</span>'
            progress_percentage = ((completed_tasks/total_task_count)*100) if total_task_count > 0 else 0
            html += f'''<div class="progress progress-sm">
                    <div class="progress-bar {progress_css[i]}" style="width: {progress_percentage}%;"></div>
                    </div>'''
    
            html += '</div>';
            i = i+1 if len(progress_css) > i else 0
                
    # html += '</div>'
    # print(html)
    return html

@frappe.whitelist()
def get_ongoing_project_contacts(project=None):
    returnData = dict()
    html = ''
    if project is None:
        html = 'Please select the ongoing project first, contacts will be loaded automatically.';
        return html
    else:
        project_doc = frappe.get_doc("Project", project)        
        tasks = frappe.db.get_list("Task", filters={'project':project_doc.name})
        
        
        
        if tasks:            
            assigned_user = set()
            for task in tasks:
                assigned_user.update(get_assigned_user("Task", task))
                
            if assigned_user:
                html += '<ul>'
                for user in assigned_user:
                    html += '<li>'+frappe.db.get_value('User', user, 'full_name')+'</li>'                                        
            html += '</ul>'   
        else:
            html = 'Tasks not assigned. Please assigned tasks and users also.'   

        returnData['html'] = html
        
        task_by_status = frappe.db.get_list('Task', filters={'project':project_doc.name},
            fields=['count(name) as count', 'status'],
            group_by='status'
        )
        
        if task_by_status:
            # returnData['chart_data'] = {}
            labels = [ status_data['status'] for status_data in task_by_status ]
            returnData['chart_data'] = { 
                "labels":labels,                       
                "datasets": [{
                    "name": "Task Statuswise",
                    "values": [ status_data['count'] for status_data in task_by_status ]
                }]
            } 
            
        returnData['activity_html'] = get_recent_activity_card(project)
        # print(returnData)
        
    return returnData
            
@frappe.whitelist()
def get_task_status_chart(project=None):
    html = ''
    if project is None:
        html = '<div id="task_status_chart">Please select the ongoing project first, contacts will be loaded automatically.</div>';        
    # else:
    
    return html


@frappe.whitelist()
def get_recent_activity_card(project=None):
    html = ''
    if project is None:
        html = 'Please select the ongoing project first, recent activity will be loaded automatically.'
    else:
        html = frappe.db.get_list('Activity Log', filters={'reference_doctype':'Task', 'timeline_doctype':'Project', 'timeline_name':project},
            fields=['subject'],
            order_by='creation DESC',
            limit_page_length=1,
        )
        
    return html 
            
    
        
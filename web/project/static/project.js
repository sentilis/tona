/*    Copyright (C) 2021  The Project TONA Authors
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

(function(window){
    function Project (){
        var self = {};
        self.Add = function (){
            var txtName = document.querySelector(".modal #project-name");
            if (txtName.value != ""){
                fetch("/api/project", {
                    method: 'post',
                    body: JSON.stringify({
                        "name": txtName.value,
                    }),
                    headers: Tona.SetHeaders(),
                }).then(response => response.json()).then(function(data){
                    var project_menu_list = document.querySelector("#project-menu-list");
                    var li = document.createElement("li");
                    li.innerHTML = '<a href="/project/'+data['payload']['id']+'">'+data['payload']['name']+'</a>';
                    project_menu_list.append(li);
                    txtName.value = ""
                    Tona.Modal.Close()
                }).catch(function(error){
                    console.error(error);
                });
            }
        };

        /*Task*/
        self.AddTask = function (e){
            var txtName = document.querySelector("#task-name");
            var txtProjectId = document.querySelector("#project-id");
            if (e.keyCode == 13 && txtName.value != "" && txtProjectId.value != ""){
                fetch("/api/project/task", {
                    method: 'post',
                    body: JSON.stringify({
                        "project_id": txtProjectId.value,
                        "name": txtName.value,
                    }),
                    headers: Tona.SetHeaders(),
                }).then(response => response.json()).then(function(data){
                    var todo_menu_list = document.querySelector("#todo-menu-list");
                    var li = document.createElement("li");
                    var taks = data['payload'];
                    li.innerHTML = '<a href="/project/'+taks['project_id']['id']+'/task/'+taks['id']+'"><input type="checkbox" class="mr-2"/>'+txtName.value+'</a>';
                    todo_menu_list.append(li);
                    txtName.value = ""
                }).catch(function(error){
                    console.error(error);
                });
                
            }            
        };

        self.EditTask = function(e, id, field, value=null){

            var data = {};
            if (e != null && value == null){
                if (Tona.IsSimpleMDE(e)){
                    data[field] = e.value();
                }else{
                    data[field]= e.target.value;
                }                
            }else if (e != null && value != null){
                data[field]= value;
            }

            let method = 'put';

            if (field == 'due') {
                var utc = new Date(new Date( data[field]).getTime());
                data[field]= utc.toISOString();
            }else if (field == 'clear-due'){
                data["due"] = null; 
                var task_due = document.querySelector("#task-due");
                if (task_due !== undefined){
                    task_due.value = ""
                }
            }else if (field == 'active'){
                data[field] = !(value === 'True');
            }else if(field == 'delete'){
                method = 'delete';
            }

            fetch("/api/project/task/"+id, {
                method: method,
                body: JSON.stringify(data),
                headers: Tona.SetHeaders(),
            }).then(response => response.json()).then(function(data){
                if (!data['ok']){
                    console.error(data)
                }
            }).catch(function(error){
                console.error(error);
            });
        }

        self.onDragStartTask = function (event){
            event
            .dataTransfer
            .setData('text/plain', event.target.parentNode.id);
            event
            .currentTarget.style.backgroundColor = 'yellow';
        }

        self.onDragOverTask = function (event) {
            event.preventDefault();
        }

        self.onDropTask = function (event) {
            var status = event.target.id.split('-')[0];
            if (status == 'todo' || status == 'doing' || status == 'review'){
                const id = event.dataTransfer.getData('text');
                const draggableElement = document.getElementById(id);
                const dropzone = event.target;          
                dropzone.nextElementSibling.appendChild(draggableElement)
                event.dataTransfer.clearData();
                var task_id =  parseInt(id.split('-')[3])
                if (task_id > 0){
                    self.EditTask(event, task_id, 'status', status)
                }
                    
            }
        }

        return self;
    }
    if (typeof(window.Project) === 'undefined'){
        window.Project = Project();
    }
})(window);
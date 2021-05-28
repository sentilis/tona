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

    function TimerAnalyze (){
        var self = {};

        self.Filters = {
            'id': 0, 
            'start_date': null, 
            'end_date': null, 
            'type': null
        };

        self.FilterBy = function(event){
            var dropdown = event.target.parentNode.parentNode.parentNode;
            var dropdownContent = dropdown.querySelector(".dropdown-content");            
            var ttype = dropdown.dataset.whoami
            if (ttype === undefined){
                return
            }
            dropdownContent.innerHTML = "";
            fetch("/api/"+ttype+"?limit=100&offset=1", {
                method: 'GET',
                headers: Tona.SetHeaders(),
            }).then(response => response.json()).then(function(data){
                if (data['ok']){
                    (data['payload'] || []).forEach(function(item, index){
                        dropdownContent.innerHTML += `
                        <a onclick="TimerAnalyze.SelectedFilterBy(event)" data-id="`+item.id+`" class="dropdown-item">`+item.name+`</a>`;
                    })
                    dropdownContent.innerHTML += `<hr class="dropdown-divider">
                    <a onclick="TimerAnalyze.SelectedFilterBy(event)" data-id="0" class="dropdown-item">All</a>`
                }
            }).catch(function(error){
                console.error(error);
            });
        }
        
        self.SelectedFilterBy = function(event){
            if (event.target.dataset.id !== null){
                self.Filters['id'] = event.target.dataset.id;
                self.Load(event);
            }
        };

        self.SelectedDate = function(event){
            if (event.target.dataset.date !== null){
                self.Filters[event.target.dataset.date] = event.target.value;
                self.Load(event)
            }
        };

        self.Load = function (event){
            var analyze_datails = document.querySelector("#analyze-details");
            var analyze_header = analyze_datails.querySelector(".menu-label")
            var analyze_list = analyze_datails.querySelector(".menu-list")

            var ttype = analyze_datails.dataset.whoami
            self.Filters['type'] = ttype;
            analyze_list.innerHTML = "";
            var id = self.Filters['id']

            fetch("/api/time-entry/analyze?"+Tona.URLQuery(self.Filters), {
                method: 'GET',
                headers: Tona.SetHeaders(),
            }).then(response => response.json()).then(function(data){
                if (data['ok']){
                    var details = data['payload'][ttype+"s"]
                    if (Object.keys(details).length > 1){
                        for (const detail_index in details){
                            var detail = details[detail_index]
                            analyze_list.innerHTML += `<li><a>`+detail[ttype].name+` 
                            <span class="is-pulled-right">`+ TonaTimeEntry.FormatDuration(detail.duration)+`</span>
                            </a></li>`
                        }
                        analyze_header.innerHTML = "General"
                    }else{
                        var detail = details[id]
                        analyze_header.innerHTML = detail[ttype].name +`<span class="is-pulled-right">`+TonaTimeEntry.FormatDuration(detail.duration)+`</span>`
                        for (const time_entry_index in detail.time_entries){
                            var time_entry = detail.time_entries[time_entry_index]
                            analyze_list.innerHTML += `<li><a>`+time_entry.name+` 
                            <span class="is-pulled-right">`+ TonaTimeEntry.FormatDuration(time_entry.duration) +`</span>
                            </a></li>`
                        }
                    }
                }
            }).catch(function(error){
                console.error(error);
            });

        }

        return self;
    }

    if (typeof(window.c) === 'undefined'){
        window.TimerAnalyze = TimerAnalyze();
    }
    
})(window);
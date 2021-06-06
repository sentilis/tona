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
if ( !Date.prototype.toISOString ) {
    ( function() {
  
        function pad(number) {
          var r = String(number);
          if ( r.length === 1 ) {
            r = '0' + r;
          }
          return r;
        }
    
        Date.prototype.toISOString = function() {
          return this.getUTCFullYear()
            + '-' + pad( this.getUTCMonth() + 1 )
            + '-' + pad( this.getUTCDate() )
            + 'T' + pad( this.getUTCHours() )
            + ':' + pad( this.getUTCMinutes() )
            + ':' + pad( this.getUTCSeconds() )
            + '.' + String( (this.getUTCMilliseconds()/1000).toFixed(3) ).slice( 2, 5 )
            + 'Z';
        };
    
      }() );
}

(function(window){
  function Tona (){
      var self = {};

      self.URLQuery = function(params){
        const esc = encodeURIComponent;
        var query = ""
        for (const param in params){
          if (params[param]){
            query += `${esc(param)}=${esc(params[param])}&`
          }
        } 
        return query
      }

      self.Notification = function(e, msg=null, type="danger", interval=5000){
        classColor = "is-danger"
        switch(type){
          case "info":
            classColor = "is-info"
            break;
          case "success":
            classColor = "is-success"
            break;
          case "warning":
              classColor = "is-warning"
              break;
          case "danger":
          default:
        }
        (document.querySelectorAll('.notification') || []).forEach(($node) => {
          var $notification = $node.parentNode;
          $notification.classList.remove('is-hidden');
          $node.classList.add(classColor);
          if (msg != null){
            $node.querySelector("#notification-content").innerHTML = msg
          }
          var $delete = $notification.querySelector(".delete");
          if ($delete != null){
            $delete.addEventListener('click', () => {
              $notification.classList.add("is-hidden");
              $node.classList.remove(classColor);
            });
            setInterval(function() {
              $notification.classList.add("is-hidden");
              $node.classList.remove(classColor);
            }, interval);
          }
        });
      }

      self.Modal = {
        modal : null,
        Close: function (){
          self.Modal.modal.classList.remove('is-active');
          self.Modal.modal = null;
        },
        Show : function(id){
          self.Modal.modal = document.getElementById(id);
          self.Modal.modal.classList.add('is-active');
          
          (self.Modal.modal.querySelectorAll('.modal-card-head .delete') || []).forEach(($delete)=>{
            $delete.addEventListener('click', self.Modal.Close);
          });
          
          (self.Modal.modal.querySelectorAll('.modal-card-foot button:not(.is-success)') || []).forEach(($delete)=>{
            $delete.addEventListener('click', self.Modal.Close);
          });
        },

      };
      
      self.Tabs = function(){
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.tabs') || []).forEach(($tabs)=>{
            ($tabs.querySelectorAll('a') || []).forEach(($a)=>{
                $a.addEventListener('click', (e)=>{
                    $ul = e.target.parentNode.parentNode;
                    var tabGroup = $ul.dataset.tabGroup;
                    var tabId = e.target.dataset.tabId;
                    $li = $ul.querySelector("li.is-active");
                    if ($li.classList != null){
                        $li.classList.remove('is-active')
                    }
                    if (e.target.parentNode.classList != null){
                        e.target.parentNode.classList.add('is-active')
                    }
                    (document.querySelectorAll("[data-tab-group-id='"+tabGroup+"']") || []).forEach(($tabContent)=>{
                      if ($tabContent.id == tabGroup+"-"+tabId){
                        $tabContent.classList.remove("is-hidden");
                      }else{
                        $tabContent.classList.add("is-hidden");
                      }
                    });
                }); 
            });        
          });
        });
      };

      self.SetHeaders = function(headers={}) {
        
        var dafaultHeaders = {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }

        if(localStorage.jwt) {
          dafaultHeaders['Authorization'] = `Bearer ${localStorage.jwt}`;
        } 
        
        return {
          ...headers,
          ...dafaultHeaders
        }

      };

      self.IsSimpleMDE = function (o){
        if (o.toTextArea !== undefined  & o.isPreviewActive !== undefined ){
          return true;
        }
        return false;
      }
      
      self.QueueSimpleMDE = {};

      self.SimpleMDE = function(){
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.textarea-markdown') || []).forEach(($md)=>{
              var simplemde = new SimpleMDE({ element: $md, forceSync: true, tabSize: 1, spellChecker: false});
              if ($md.onblur !== null ){            
                  simplemde.codemirror.on("blur", function(event){
                      $md.onblur(simplemde)            
                  });
              }
              if ($md !== ''){
                self.QueueSimpleMDE[$md.id] = simplemde;
              }
          });
        });
      }

      self.Dropdown = function (){
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.dropdown') || []).forEach((dropdown)=>{
            dropdown.addEventListener('click', (e)=>{
              var isActive = false;
              if (dropdown.classList && dropdown.classList.length > 0){
                  for (var a = 0  ;  a < dropdown.classList.length; a++){
                      if (dropdown.classList[a] == 'is-active'){
                          isActive = true;
                      }
                  }
              }
              if (isActive){
                  dropdown.classList.remove("is-active");
              }else{
                dropdown.classList.add("is-active");
              }
            });
          }); 
        });
      }
      

      
      /** Widget Comment */
      self.WidgetComment = function(event){
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.widget-comment') || []).forEach((wc)=>{
            let content = `
              <article class="media widget-comment-header">
                <div class="media-content">
                  <div class="field">
                    <p class="control">
                      <textarea class="textarea" rows="2" placeholder="Add a comment..."></textarea>
                    </p>
                  </div>
                  <div class="field">
                    <p class="control is-inline">
                      <button class="button is-small" onclick="Tona.PostComment(event)">Post comment</button>
                    </p>
                  </div>
                </div>
              </article>
      
              <article class="media widget-comment-content">
                <div class="media-content">
                  <a onclick="Tona.LoadComment(event, 1)" class="comment-show-more">Show More</a>
                </div>
              </article>  
            `;
            wc.innerHTML = content;
          });
        });
      }

      self.PostComment = function (event){
        let doc = event?.target?.parentNode?.parentNode?.parentNode?.parentNode?.parentNode
        let model = doc?.dataset?.commentResModel;
        let id = doc?.dataset?.commentResId;
        if (doc !== null && model !== null && id !== null){
          let content = doc.querySelector(".textarea");
          if (content !== null){
            let data  = { content: content.value, res_model: model, res_id: parseInt(id)}
            fetch("/api/comment",{ 
                method:'post', 
                body: JSON.stringify(data),
                headers: self.SetHeaders()
              }
            ).then(response => response.json()).then(function(data){
              if (data['ok']){
                  content.value = "";
                  self.LoadComment(event)
              }
          }).catch(function(error){
              console.error(error);
          });
          }
        }
      }

      self.LoadComment  = function (event, offset=1){
        let doc = event?.target?.parentNode?.parentNode?.parentNode?.parentNode?.parentNode       
        let model = doc?.dataset?.commentResModel;
        if (model === undefined){
          doc = event?.target?.parentNode?.parentNode?.parentNode
          model = doc?.dataset?.commentResModel;
        }
        let id = doc?.dataset?.commentResId;

        let content = doc.querySelector(".widget-comment-content > .media-content");
        if ( content !== null){
          if (offset == 1){
            content.innerHTML = "";
          }
          fetch("/api/comment?model="+model+"&id="+id+"&offset="+offset+"&limit=5", {
            method: 'get',
            headers: self.SetHeaders(),
          }).then(response => response.json()).then(function(data){
              if (data['ok']){
                  let payload = data['payload'] || [];
                  if (payload.length > 0){
                      for ( a = 0 ; a  < payload.length; a++ ){
                          let record = payload[a]
                          content.innerHTML += `
                            <div class="content">
                            <p>
                              `+record['content']+`
                              <a onclick="Tona.DeleteComment(event,`+record['id']+`)" class="is-small is-pulled-right">
                                <i class="fas fa-trash"></i>
                              </a>
                              <br>
                              <small>`+record['created_at']+` </small>
                            </p>
                            
                          </div>`;
                      }
                      if (offset != 1){
                          content.querySelector(".comment-show-more").remove()
                      }
                      content.innerHTML +=`<a onclick="Tona.LoadComment(event,`+(offset+1)+`)" class="comment-show-more">Show More</a>`;
                  }else{
                      let csm = content.querySelector(".comment-show-more")
                      if (csm !== null){
                        csm.remove();
                        content.innerHTML +=`<a onclick="Tona.LoadComment(event, 1)" class="comment-show-more">Show less</a>`;
                      }
                      
                  }
              }
          }).catch(function(error){
              console.error(error);
          });
        }
      }

      self.DeleteComment = function(event, id){
        let content = event?.target?.parentNode?.parentNode?.parentNode;
        if  (content !== null){
          fetch("/api/comment/"+id, {
            method: 'delete',
            headers: self.SetHeaders(),
          }).then(response => response.json()).then(function(data){
            if (data['ok']){
              content.remove()
            }
          }).catch(function(error){
              console.error(error);
          });

        }
      };

      /* Widget Attachment*/
      self.WidgetAttachment = function(event){
        document.addEventListener("DOMContentLoaded", function(event) {
          (document.querySelectorAll('.widget-attachment') || []).forEach((wa)=>{
              let content = `
                <div class="file has-name is-fullwidth is-small widget-attachment-header">
                  <label class="file-label">
                    <input onchange="Tona.UploadAttachment(event)" class="file-input" type="file">
                    <span class="file-cta">
                      <span class="file-icon">
                        <i class="fas fa-upload"></i>
                      </span>
                      <span class="file-label">
                        Choose a file…
                      </span>
                    </span>
                    <span class="file-name">
                      No file uploaded
                    </span>
                  </label>
                </div>
                <article class="media"></article>
                <article class="media widget-attachment-content">
                  <div class="media-content">
                    <a onclick="Tona.LoadAttachment(event, 1)" class="attachment-show-more">Show More</a>
                  </div>
                </article>`;
                wa.innerHTML = content;
          });
        });

      }
      
      self.AttchementBase64 = function (file) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => resolve(reader.result);
          reader.onerror = error => reject(error);
        });
      }

      self.UploadAttachment = function(event){
        let fileInput = event?.target;
        let doc = fileInput?.parentNode?.parentNode?.parentNode;
        let model = doc?.dataset?.attachmentResModel;
        let id = doc?.dataset?.attachmentResId;
        if (id !== null && model !== null && doc !== null && fileInput.files.length > 0) {
          let file = fileInput.files[0]
          let fileName = doc.querySelector(".file-name")
          if (fileName !== null){
            fileName.textContent = file.name;
          }
          self.AttchementBase64(file).then((content)=>{
            console.log(content)
            let contentList = content.split(";base64,");
            let data = {
              'content':  contentList[1],
              'res_model': model,
              'res_id': parseInt(id), 
              'name': file.name,
              'mime': file.type,
            }
            fetch('/api/attachment',{ 
              method:'post', 
              body: JSON.stringify(data),
              headers: self.SetHeaders({'Content-Length': file.size})
            }
            ).then(response => response.json()).then(function(data){
              if (data['ok']){
                fileName.textContent = "";
                fileInput.value = "";
                self.LoadAttachment(event)
              }
            }).catch(function(error){
                console.error(error);
            });
          });
        }
      }

      self.LoadAttachment  = function (event, offset=1){
        let doc = event?.target?.parentNode?.parentNode?.parentNode;         
        let model = doc?.dataset?.attachmentResModel;
        if (model === undefined){
          doc = event?.target?.parentNode?.parentNode?.parentNode
          model = doc?.dataset?.attachmentResModel;
        }
        let id = doc?.dataset?.attachmentResId;
        let content = doc.querySelector(".widget-attachment-content > .media-content");
        if ( content !== null){
          if (offset == 1){
            content.innerHTML = "";
          }
          fetch("/api/attachment?model="+model+"&id="+id+"&offset="+offset+"&limit=5", {
            method: 'get',
            headers: self.SetHeaders(),
          }).then(response => response.json()).then(function(data){
              if (data['ok']){
                  let payload = data['payload'] || [];
                  if (payload.length > 0){
                      for ( a = 0 ; a  < payload.length; a++ ){
                          let record = payload[a]
                          content.innerHTML += `
                            <div class="content">
                            <p>
                              `+record['name']+`
                              <a onclick="Tona.DeleteAttachment(event,`+record['id']+`)" class="ml-5 is-small is-pulled-right">
                                <i class="fas fa-trash"></i>
                              </a>
                              <a href="/api/attachment/preview/`+record['id']+`" target="_blank" class="ml-4 is-small is-pulled-right">
                                <i class="fas fa-external-link-alt"></i>
                              </a>
                              <a href="/api/attachment/download/`+record['id']+`" target="_blank" class="ml-4 is-small is-pulled-right">
                                <i class="fas fa-download"></i>
                              </a>
                              <br>
                              <small>`+record['created_at']+` </small>
                            </p>                            
                          </div>`;
                      }
                      if (offset != 1){
                          content.querySelector(".attachment-show-more").remove()
                      }
                      content.innerHTML +=`<a onclick="Tona.LoadAttachment(event,`+(offset+1)+`)" class="attachment-show-more">Show More</a>`;
                  }else{
                      let csm = content.querySelector(".attachment-show-more")
                      if (csm !== null){
                        csm.remove();
                        content.innerHTML +=`<a onclick="Tona.LoadAttachment(event, 1)" class="attachment-show-more">Show less</a>`;
                      }
                      
                  }
              }
          }).catch(function(error){
              console.error(error);
          });
        }
      }

      self.DeleteAttachment = function(event, id){
        let content = event?.target?.parentNode?.parentNode?.parentNode;
        if  (content !== null){
          fetch("/api/attachment/"+id, {
            method: 'delete',
            headers: self.SetHeaders(),
          }).then(response => response.json()).then(function(data){
            if (data['ok']){
              content.remove()
            }
          }).catch(function(error){
              console.error(error);
          });

        }
      };

      return self;
  }

  if (typeof(window.Tona) === 'undefined'){
    window.Tona = Tona();
  }
})(window);

/** Auto apply styles | accions */
( function() {
  Tona.Dropdown();
  Tona.Tabs();
  Tona.SimpleMDE();
  Tona.WidgetAttachment(null);
  Tona.WidgetComment(null);

}() );
      function fileSelected() {
        var file = document.getElementById('fileToUpload').files[0];
        if (file) {
            var info = "";
          if (file.name.toLowerCase().indexOf('.xls')  == -1){
            info = "只能上传扩展名为.xls的电子表格文件！";
          };
          var max_size =parseInt (document.getElementById('upload_max_size').value);
          if ((Math.round(file.size * 100 / (1024 * 1024)) / 100) > max_size){
            info = info + "上传文件过大！";
          };
          if (info == ""){
              var fileSize = 0;
              if (file.size > 1024 * 1024)
                fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
              else
                fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

              document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
              document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
              document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
          }else{
            document.getElementById('uploadform').reset();
            alert(info);
            location.reload();
          }
        }
      }

      function uploadFile() {
        var fd = new FormData();
        // fd.append('_xsrf',document.getElementsByName('_xsrf')[0].value);
        fd.append("myfile", document.getElementById('fileToUpload').files[0]);
        var xhr = new XMLHttpRequest();
        xhr.upload.addEventListener("progress", uploadProgress, false);
        xhr.addEventListener("load", uploadComplete, false);
        xhr.addEventListener("error", uploadFailed, false);
        xhr.addEventListener("abort", uploadCanceled, false);
        xhr.open("POST",document.getElementById('posturl').value);
        xhr.send(fd);
      }

      function uploadProgress(evt) {
        if (evt.lengthComputable) {
          var percentComplete = Math.round(evt.loaded * 100 / evt.total);
          document.getElementById('myuploadprogress').style.width=percentComplete.toString() + '%';
          document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
        }
        else {
          document.getElementById('progressNumber').innerHTML = 'unable to compute';
        }
      }

      function uploadComplete(evt) {
        /* This event is raised when the server send back a response */
        alert(evt.target.responseText);
      }

      function uploadFailed(evt) {
        alert("There was an error attempting to upload the file.");
      }

      function uploadCanceled(evt) {
        alert("The upload has been canceled by the user or the browser dropped the connection.");
      }
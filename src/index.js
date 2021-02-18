import 'react-dropzone-uploader/dist/styles.css'
import Dropzone from 'react-dropzone-uploader'
import ReactDom from 'react-dom';
import {saveAs} from "file-saver";
import { v1 as uuidv1 } from 'uuid';
import { useState } from 'react';


const MyUploader = () => {
  // specify upload params and url for your files

  const [count, setCount] = useState(0);

  

  const getUploadParams = ({file, meta }) => { 

  	let id = 0;
  	if (count == 0){
  		id = uuidv1();
  		setCount(id);
  		alert(id)
  	}else{
  		id = count;
  	}

  	
 
  	
  
  	const body = new FormData()
  	body.append('file', file)
  	body.append('session_id', id)
    return { url: '/upload', body} 
  	
  }
  
  // called every time a file's `status` changes
  const handleChangeStatus = ({ meta, file }, status) => { console.log(status, meta, file) }
  
  // receives array of files that are done uploading when submit button is clicked
  const handleSubmit = (files, allFiles) => {
  	const body = new FormData();

  	body.append('session_id', count);
  	fetch("/joinPdf",{method:"POST",body:body}) .then(function (response) {
                    return response.blob();
                }
            )
            .then(function(blob) {
                saveAs(blob, "yourFilename.pdf");
            }).then(function (data) {

				const body_2 = new FormData();

  				body_2.append('session_id', count);

				// Fetch another API
				return fetch('/DelSession',{method:"POST",body:body_2	});

			});

    allFiles.forEach(f => f.remove())
    setCount(0);
  }

  return (
    <Dropzone
      getUploadParams={getUploadParams}
      onChangeStatus={handleChangeStatus}
      onSubmit={handleSubmit}
      accept=".pdf"
    />
  )
}







ReactDom.render(<MyUploader />, document.getElementById('root'));

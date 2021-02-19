import 'react-dropzone-uploader/dist/styles.css'
import Dropzone from 'react-dropzone-uploader'
import ReactDom from 'react-dom';
import {saveAs} from "file-saver";
import { v1 as uuidv1 } from 'uuid';
import { useState } from 'react';
import './index.css'
import { Navbar, Nav, NavDropdown, Form, FormControl, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const MyUploader = () => {
  // specify upload params and url for your files

  const [count, setCount] = useState(0);

  

  const getUploadParams = ({file, meta }) => { 

  	let id = 0;
  	if (count == 0){
  		id = uuidv1();
  		setCount(id);
  	}else{
  		id = count;
  	}

  	
 
  	
  
  	const body = new FormData()
  	body.append('file', file)
  	body.append('session_id', id)
    return { url: '/upload', body} 
  	
  }
  
  // called every time a file's `status` changes
  const handleChangeStatus = ({ meta, file }, status) => { //console.log(status, meta, file) 
  	console.log(status, file.name) 
  	if (status == 'removed'){
	  	const body = new FormData();
		body.append('session_id', count);
		body.append('file_name', file.name);
	  	fetch("/DelSingleFile",{method:"POST",body:body})

  	}
  }
  
  // receives array of files that are done uploading when submit button is clicked
  const handleSubmit = (files, allFiles) => {
  	const body = new FormData();

  	body.append('session_id', count);
  	fetch("/joinPdf",{method:"POST",body:body}).then(function (response) {
                    return response.blob();
                }
            )
            .then(function(blob) {
                saveAs(blob, "yourFile.pdf");
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

  	<section>
  		<Navbar bg="light" expand="lg">
  <Navbar.Brand href="#home">PDF Tools</Navbar.Brand>
  <Navbar.Toggle aria-controls="basic-navbar-nav" />
  <Navbar.Collapse id="basic-navbar-nav">
    <Nav className="mr-auto">
      <Nav.Link href="#home">Join</Nav.Link>
     
    </Nav>
   
  </Navbar.Collapse>
</Navbar>
    <Dropzone
      getUploadParams={getUploadParams}
      onChangeStatus={handleChangeStatus}
      onSubmit={handleSubmit}
      accept=".pdf"
    />
    </section>
  )
}







ReactDom.render(<MyUploader />, document.getElementById('root'));

import 'react-dropzone-uploader/dist/styles.css'
import Dropzone from 'react-dropzone-uploader'
import ReactDom from 'react-dom';
import {saveAs} from "file-saver";
import { v1 as uuidv1 } from 'uuid';
import { useState } from 'react';
import './index.css';
import packageJson from '../package.json';
import { Form, Button} from 'react-bootstrap';


function SubmitForm(props){

  const [extractAll, setAll] = useState(false);
  const [range, setRange] = useState("");
  const [submit, setSubmit] = useState(false);

  const extractAllOnChange = (event) =>{
    console.log(event.target.checked);
    setAll(event.target.checked);
    console.log(extractAll);
  }

  const rangeOnChange = (event) =>{
    console.log(event.target.value);
    setRange(event.target.value);
  }

  const handleSubmit = () =>{
    const body = new FormData();
    alert(submit);

    body.append('session_id', props.count);
    body.append('extract_all', extractAll);
    body.append('range', range);
    fetch("/downloadSplitedPdf",{method:"POST",body:body}).then(function (response) {
                    return response.blob();
                }
            )
            .then(function(blob) {
                saveAs(blob, "splitedFiles.zip");
            }).then(function (data) {

        const body_2 = new FormData();

          body_2.append('session_id', props.count);

        // Fetch another API
        return fetch('/DelSession',{method:"POST",body:body_2 });
        
        
       

      });

      setSubmit(true);
  }

  if(props.count != 0){
    return (
      <Form  style= {{display: "inline-block"}}>
        <Form.Group controlId="formBasicCheckbox">
        <Form.Check checked={extractAll} onChange={extractAllOnChange} type="checkbox" label="Each Pages in Single File" />
        </Form.Group>
        <Form.Group controlId="formBasicEmail">
        <Form.Label>Split Range</Form.Label>
        <Form.Control type="text" placeholder="Range" onChange={rangeOnChange} />
      </Form.Group>
      <Button disabled={submit} onClick={handleSubmit} variant="primary" >
        Split
      </Button>
    </Form>
    )

  }else{
    return ("")
  }
  
}

function SplitPDF (props) {
  // specify upload params and url for your files

  const [count, setCount] = useState(0);
  const [items, setItems] = useState([]);

  

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
    return { url: '/splitUpload', body} 
    
  }
  
  // called every time a file's `status` changes
  const handleChangeStatus = ({ meta, file, remove }, status) => { //console.log(status, meta, file) 
    console.log(status, file.name) 
    if (status === 'headers_received') {
      remove();
    }
    
    if (status == 'done'){
      const body = new FormData();
      body.append('session_id', count);
      body.append('file_name', file.name);
      fetch("/getImagePages",{method:"POST",body:body}).then(res => res.json()).then(data => {
      console.log(data);
      setItems(data);
    });

    }
  }

  return (
    <div>
      <Dropzone
        getUploadParams={getUploadParams}
        onChangeStatus={handleChangeStatus}
        accept=".pdf"
        maxFiles={1}
        multiple={false}
        canCancel={false}
      />
      {items.map((item) => (
        <div style={{width: "150px", height: "200px",  float: "left", margin: "20px",
              backgroundClip: "border-box", backgroundColor: "#ff0",
              borderWidth: "10px"}}>
              <img src={packageJson.proxy+"/image?id="+count+"&n="+item}  width="150px" height="200px"></img>
        </div>))}

        <SubmitForm count={count}/>

        
    </div>

   
  )
}

export default SplitPDF;



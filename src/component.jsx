
import './App.css';
import org from "./assets/original.jpg"
import qimg from "./assets/qimage.jpg"
import no_img from "./assets/no_img.jpg"

import React, { useState } from 'react'
import axios from 'axios'



function Component1() {

  const[image, setImage] = useState(no_img)
  const[query, setQuery] = useState('')
  const[detected, setDetected] = useState()
  const[display, setDisplay] = useState()
  const[qimage, setQimage] = useState(0)

  const[disabled, setDisabled] = useState(false)

  // const[url, setUrl] = useState('')




  const changed = async(e)=>
    {
        
        try {
          const formData = new FormData();
          formData.append('original', e.target.files[0]);
    
          const response = await axios.post('/upload/original', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          console.log('Image uploaded successfully:', response.data);
          setDetected(true)
          setDisplay(true)
          setImage(no_img)
          setDisabled(false)
          setQimage(0)
        } catch (error) {
          console.error('Error uploading image:', error);
        }
    }

    const changed_qimage = async(e) =>
      {
        try{
          const data = new FormData();
          data.append('qimage', e.target.files[0]);

          const response = await axios.post('/upload/qimage', data,{
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          console.log('Query_image uploaded successfully:', response.data);
          setDetected(true)
          setDisplay(true)
          setImage(no_img)
          setQuery('')
          setDisabled(true)
          setQimage(1)
        } catch (error) {
          console.error('Error uploading Qimage:', error);
        }
      }


    
  const handleQuery = (e) => 
    {
      setDisplay(true)
      setDetected(true)
      setQuery(e.target.value)
      setImage(no_img)

    };

  const handleSubmit = async(e) =>
    {

      try {
        const formData1 = new FormData();
        formData1.append('query', query);
        formData1.append('qimage', qimage);
  
        const response = await axios.post('/generate', formData1, 
          {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // console.log('FormData:', formData1.get('query'));
        console.log('Query uploaded Successfully', response.data);
        setDisplay(false)
        setDetected(response.data.detected)
        setImage(response.data.image);
        
        // console.log(object)
      } catch (error) {
        console.error('Error uploading query:', error);
      }
      
    }
    

  return (
    <div className="App">
      <h1>Object Finder</h1>
      <div className="box">
        {/* <img src={org} alt="" /> */}
        
        <div className="left">
          <div style={{backgroundImage: `url(${org})`}}  className="original"></div>
          <input type="file" onChange={changed} id = "upload"/>
          <input disabled = {disabled} placeholder='Enter Objects' className='text' type="text" value={query} onChange={handleQuery}/>
          <input  type="file" onChange={changed_qimage}  id = "query_img"/>
          <label htmlFor="query_img">Query Image</label>
          <div className="buttons">
          <label htmlFor="upload">SELECT IMAGE</label>
          <button onClick={handleSubmit}>SUBMIT</button>
          </div>
        </div>
        <div className="line1"></div>
        <div className="line2"></div>
        <div className="result">
        <div style={qimage? {backgroundImage: `url(${qimg})`} : {backgroundImage: `none`}}  className="query">
          {qimage? "" : <p>No Query Image</p>}
        </div>
        <div className="right">
        {detected? <img className = "detected" src={display? image : `data:image/jpeg;base64,${image}`} alt ="no img"/> : <p>No Objects Detected</p>}
        </div>
        </div>
      </div>
    </div>
  )
}

export default Component1

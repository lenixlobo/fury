from fury import actor, window
import vtk
import numpy as np
from fury.utils import rgb_to_vtk

#Create  a Scene
scene = window.Scene()
scene.background((1.0, 0.8, 0.8))


#Create a Texture
texture = vtk.vtkTexture()
texture.CubeMapOn()
#Noise texture
arr =  np.random.randn(64, 164, 4)

grid = rgb_to_vtk(arr.astype(np.uint8))
for i in range(6):
	texture.SetInputDataObject(i, grid)

#Create an sphere

sphere = vtk.vtkSphereSource()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(100)
sphere.SetRadius(3)

sphereMapper = vtk.vtkOpenGLPolyDataMapper()
sphereMapper.SetInputConnection(sphere.GetOutputPort())

sphereActor = vtk.vtkActor()
sphereActor.SetMapper(sphereMapper)

sphereActor.SetTexture(texture)


# // Add new code in default VTK vertex shader
sphereMapper.AddShaderReplacement(
    vtk.vtkShader.Vertex,
    "//VTK::PositionVC::Dec",  # replace the normal block
    True,  # before the standard replacements
    """
    //VTK::PositionVC::Dec  // we still want the default
    out vec3 TexCoords;
    """,
    False  # only do it once
)

sphereMapper.AddShaderReplacement(
    vtk.vtkShader.Vertex,
    "//VTK::PositionVC::Impl",  # replace the normal block
    True,  # before the standard replacements
    """
    //VTK::PositionVC::Impl  // we still want the default
    vec3 camPos = -MCVCMatrix[3].xyz * mat3(MCVCMatrix);
    //TexCoords.xyz = reflect(vertexMC.xyz - camPos, normalize(normalMC));
    //TexCoords.xyz = normalMC;
    TexCoords.xyz = vertexMC.xyz;

    """,
    False  # only do it once
)


sphereMapper.SetGeometryShaderCode("""
	//VTK::System::Dec
    //VTK::PositionVC::Dec

    // declare coordinate transformation matrices
    
		uniform mat4 MCDCMatrix; // - gl_modelviewprojectionmatrix
        uniform mat4 MCVCMatrix; // - gl_modelview_matrix (model to view)
        uniform mat4 WCMCMatrix; // - world to model
        uniform mat4 MCWCMatrix; // - model to world
        uniform mat4 MCPCMatrix; // - model to projection
        uniform mat4 WCVCMatrix; // - world to view - half of the camera transform
        uniform mat4 WCPCMatrix; // - world to projection
        uniform mat4 VCPCMatrix; // - view to projection - the other part of the camera transform
        uniform mat4 VCDCMatrix; // - projection matrix

    //VTK::PrimID::Dec

    //VTK::Color::Dec
    //VTK::Normal::Dec
    //VTK::Light::Dec
    //VTK::TCoord::Dec
    //VTK::Picking::Dec
    //VTK::DepthPeeling::Dec
    //VTK::Clip::Dec
    //VTK::Output::Dec

    layout (triangles) in;
    layout (triangle_strip, max_vertices = 120) out;

    int fur_layers = 30;
    float fur_depth = 5.0;

     void main(){

	    int i, layer;
	    float disp_delta = 1.0 / float(fur_layers);
	    float d = 0.0;
	    vec4 position;

	    for(layer = 0; layer < fur_layers; layer++)
	    {
	    		//Calulate the Normal for a given face

	    		vec3 p0 = gl_in[0].gl_Position.xyz;
	    		vec3 p1 = gl_in[1].gl_Position.xyz;
	    		vec3 p2 = gl_in[2].gl_Position.xyz;

	    		vec3 v0 = p0 - p1;
	    		vec3 v1 = p2 - p1;

	    		vec3 norm = cross(v1, v0);
	    		norm = normalize(norm);

	    	// For each incoming vertex (should be three of them) 
	    	for(i = 0; i < gl_in.length(); i++)
	    	{
	 			vec4 displacement = vec4(norm * d * fur_depth, 0.0);
	    		position = gl_in[i].gl_Position + displacement;
	    		
	    		//I think the issue lies here	
	    		//gl_Position = projection_matrix * (model_matrix * position);
	    		
	    		gl_Position = gl_in[i].gl_Position ;
	    		//vertexVCGSOutput = vertexVCVSOutput[i] + gl_Position;
	    		EmitVertex();
	    	}

	    	d += disp_delta;
	    	EndPrimitive();
	    }

    }
	"""
	)


sphereMapper.SetFragmentShaderCode(
    """
    //VTK::System::Dec  // always start with this line
    //VTK::Output::Dec  // always have this line in your FS
    in vec3 TexCoords;
    uniform samplerCube texture_0;

    uniform vec4 fur_color = vec4(0.3, 0.3, 0.3, 1.0);


    void main() {

    	vec4 rgba = texture(texture_0, TexCoords);
    	float  t = rgba.a;
    	gl_FragData[0] = fur_color * vec4(1.0, 1.0, 0.3, t);
        //gl_FragData[0] = texture(texture_0, TexCoords);
    }
    """
)


scene.add(sphereActor)
#Callback 

window.show(scene, size=(1960, 1200))
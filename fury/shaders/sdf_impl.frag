/* SDF fragment shader implementation */

//VKT::Light::Impl

vec3 point = centeredVertexMC;

vec3 uu = vec3(MCVCMatrix[0][0], MCVCMatrix[1][0], MCVCMatrix[2][0]); // camera right
vec3 vv = vec3(MCVCMatrix[0][1], MCVCMatrix[1][1], MCVCMatrix[2][1]); //  camera up
vec3 ww = vec3(MCVCMatrix[0][2], MCVCMatrix[1][2], MCVCMatrix[2][2]); // camera direction

//ray origin
vec4 ro = -MCVCMatrix[3] * MCVCMatrix;  // camera position in world space

//ray direction
vec3 rd = normalize(point - ro.xyz);

float t = castRay(ro.xyz, rd);
    
if(t < 20.0)
{
    vec3 position = ro.xyz + t * rd;
    vec3 norm = calculateNormal(position);

    fragOutput0 = vec4( norm, 1.0);
    	
}
else{
    fragOutput0 = vec4(0, 0, 0, 0.3);
    //discard;
}

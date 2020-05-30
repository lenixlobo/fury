/* SDF fragment shader declaration */

//VTK::ValuePass::Dec

in vec3 centeredVertexMC;

uniform mat4 MCVCMatrix;


float sdTorus(vec3 p, vec2 t)
{
	vec2 q = vec2(length(p.xz) - t.x, p.y);
	return length(q) - t.y;
}

float map(in vec3 position)
{
	float d1 = sdTorus(position, vec2(0.4, 0.1));
	return d1;
}

vec3 calculateNormal(in vec3 position)
{
	vec2 e = vec2(0.0001, 0.0);
	return normalize( vec3( map(position + e.xyy) - map(position - e.xyy),
							map(position + e.yxy) - map(position - e.yxy),
							map(position + e.yxx) - map(position - e.yyx)
						)
					);
}

float castRay(in vec3 ro, vec3 rd)
{
	float t = 0.0;
	for(int i=0; i<400; i++){

		vec3 position = ro + t * rd;
		vec3 norm = calculateNormal(position);

		float h = map(position);
		if(h<0.0001) break;

		t += h;
		if (t>20.0) break;
	}

	return t;
}

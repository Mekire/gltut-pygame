#version 330

out vec4 outputColor;

uniform float frag_period;
uniform float time;

const vec4 firstColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
const vec4 secondColor = vec4(0.0f, 1.0f, 0.0f, 1.0f);

void main()
{
	float currTime = mod(time, frag_period);
	float currLerp = currTime / frag_period;

	outputColor = mix(firstColor, secondColor, currLerp);
}

#version 330

out vec4 outputColor;

void main()
{
    float lerp_value = gl_FragCoord.y / 500.0f;
	outputColor = mix(vec4(1.0f, 0.0f, 1.0f, 1.0f), vec4(0.0f, 1.0f, 0.0f, 1.0f), lerp_value);
}

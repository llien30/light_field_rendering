from lightfield import (
    bulldozer_light_field_renderer,
    bulldozer_light_field_renderer_rotate,
    make_bulldozer_data,
)

rectified_data = make_bulldozer_data()
print("Finished Load Data!")

for z in range(-5, 6):
    bulldozer_light_field_renderer(
        0.5,
        0.5,
        z * 0.1,
        0.5,
        rectified_data,
        f"./video_image/{z+5}.png",
    )
    print("image saved!")

for i in range(20):
    bulldozer_light_field_renderer_rotate(
        0.3 * i, 0.3, 0.5, rectified_data, f"./rotate_sample/{i}.png"
    )

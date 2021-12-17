from math import ceil, sqrt

target_x_min, target_x_max = 155, 182
target_y_min, target_y_max = -117, -67


def simulate(vx: int, vy: int) -> bool:
    x, y = 0, 0
    while True:
        # update step
        x += vx
        y += vy
        if vx < 0:
            vx += 1
        elif vx > 0:
            vx -= 1
        vy -= 1

        # check if hit target
        if target_x_min <= x <= target_x_max and target_y_min <= y <= target_y_max:
            return True

        # check if over- or undershoot
        if (
            (x > target_x_max)
            or (vx == 0 and x < target_x_min)
            or (vy <= 0 and y < target_y_min)
        ):
            return False


n_hits = 0

# for initial velocity of vx0, position x will stop changing upon reaching
# 1 + 2 + ... + vx0 = vx0 * (vx0 + 1) / 2
# if we try to hit target_x_min, solving for vx0 gives us
# bound = -0.5 +/- sqrt(0.25 + 2 * target_x_min)
vx0_lower_bound = ceil(-0.5 + sqrt(0.25 + 2 * target_x_min))
# if we have vx0 > target_x_max, we will always overshoot
vx0_upper_bound = target_x_max
for vx0 in range(vx0_lower_bound, vx0_upper_bound + 1):
    # as lower bound we can simply chose target_y_min, or we undershoot
    vy0_lower_bound = target_y_min
    # after going up, we always hit y=0 again, exactly after 2*vx + 2 steps
    # the velocity at that point will be -vy0 - 1
    # that means the next y will also be -vy0 - 1
    # the higest y will be reached by having the largest initial vy0 that still lets us hit the target
    # so to hit the target at the lowest point, we need target_y_min = -vy0 - 1
    # so we simulate up to vy0 = -1 - target_y_min
    vy0_upper_bound = -1 - target_y_min
    for vy0 in range(vy0_lower_bound, vy0_upper_bound + 1):
        if simulate(vx0, vy0):
            n_hits += 1

print("Solution:", n_hits)

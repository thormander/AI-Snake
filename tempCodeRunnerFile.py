        # case of corners going vetical
        if previous_segment.x == current_segment.x:
            # body going down
            if next_segment.x > current_segment.x:
                if next_segment.y > current_segment.y:
                    return self.body_bottomright # curve right
                else:
                    return self.body_bottomleft # curve left
            # body going up
            else:
                if next_segment.y > current_segment.y:
                    return self.body_bottomleft # curve right
                else:
                    return self.body_topleft # curve left                

        # case of corners going horizontal
        else:
            # body going right
            if next_segment.y > current_segment.y:
                if previous_segment.x < current_segment.x:
                    return self.body_bottomright # curve down
                else:
                    return self.body_bottomleft # curve up
            # body going left
            else:
                if previous_segment.x < current_segment.x:
                    return self.body_topright # curve down
                else:
                    return self.body_topleft # curve up
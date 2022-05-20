import pyrealsense2.pyrealsense2 as rs

class DCCADepthFilterManager:
    def __init__(self):
        self.depth2disparity = rs.disparity_transform(True)
        self.disparity2depth = rs.disparity_transform(False)

    def apply_DepthFilter(self, depth_frame, filterType = None):
        """
        Applying preprocessing filters on depth_frame # BEWARE : not on depth_ColorMap!
        """
        if filterType =='decimation':
            """
            [ Decimation Filter ]
            - reduce spatial resolution  == reduce depth scene complexity
            - WHILE preserving z-accuracy and performing some rudamentary hole-filling
            - with scale factor 3: [1280, 720]/3 -> [428, 240] (scale factor range : 2 ~ 8)
            - zero filling padding
            """
            decimated_depth = self._decimation_filter(depth_frame)
            return decimated_depth

        if filterType == 'spatial':
            """
            [ Spatial Filter ]
            - aka Domain-Transformation Edge Preserving Smoothing
            - 1D edge-preserving spatial filter using high-order domain transform
            - linear time compute, not affected by the choice of params
            - params = {
                filter magnitude : #filter_iterations (1 ~ 5) default 2,
                Smooth alpha : exponential moving average with (Alpha = 1 - no filter) ~ (Alpha = 0 - infinite filter) range(0.25 ~ 1) default 0.5,
                Smooth delta : Step-size boundary = how much should I preserve edges (1 ~ 50) default 20,
                Hole Filling : heuristic symmetric hole-filling (0 ~ 5) default 0
            }
            """
            spatial_filtered_depth = self._spatial_filter(depth_frame)
            return spatial_filtered_depth

        if filterType == 'temporal':
            """
            [ Temporal Filter ]
            - improving depth data persistencyt6 by manipulating per-pixel values based on previous frames history (+updating)
            - if missing/invalid : apply user-defined persistency mode
            - great reliance to historic data -> best suited for static scenes!
            - params = {
                Smooth alpha : exponential moving average with (Alpha = 1 - no filter) ~ (Alpha = 0 - infinite filter) range(0 ~ 1) default 0.4,
                Smooth delta : Step-size boundary = how much should I preserve surfaces/edges (1 ~ 100) default 20,
                Persistency Index : predefined rule that governs invalid data. Differ mode by mode (details in librealsense github) range(0 ~ 8) default 3
            }
            """
            temporal_filtered_depth = self._temporal_filter(depth_frame)
            return temporal_filtered_depth

        if filterType == 'holefilling':
            """
            [ Hole Filling Filter ]
            - Rectify missing data with N4-neighbors : select one of them under user-defined rule
            - range(0 ~ 2) = {
                0 : fill_from_left = use the value from the left neighbor,
                1 : farest_from_around = use the value from the N4 which is FURTHEST away from the sensor, (default)
                2 : nearest_from_around = use the value from the N4 which is CLOSEST away from the sensor
            }
            """
            hole_filled_depth = self._holefilling_filter(depth_frame)
            return hole_filled_depth

        if filterType == None:
            """
            [ Applying with disparity transformation ]
            
            ** recall : disparity = difference beteween 2 stereo cams
            """

            frame = depth_frame
            frame = self._decimation_filter(frame)
            frame = self.depth2disparity.process(frame)
            frame = self._spatial_filter(frame)
            frame = self._temporal_filter(frame)
            frame = self.disparity2depth.process(frame)
            frame = self._holefilling_filter(frame)

            return frame




    def _decimation_filter(self, depth_frame):
        decimation = rs.decimation_filter()
            
        # decimation.set_option(rs.option.filter_magnitude, 4) #default scale factor = 2

        decimated_depth = decimation.process(depth_frame)
        return decimated_depth

    def _spatial_filter(self, depth_frame):
        spatial = rs.spatial_filter()
        
        # spatial.set_option(rs.option.filter_magnitude, 5)
        # spatial.set_option(rs.option.filter_smooth_aplha, 1)
        # spatial.set_option(rs.option.filter_smooth_delta, 40) # my tip: increasing alpha, delta increases the filter effect!
        

        spatial_filtered_depth = spatial.process(depth_frame)

        return spatial_filtered_depth

    def _temporal_filter(self, depth_frame):
        temporal = rs.temporal_filter()
        temporal_filtered_depth = temporal.process(depth_frame)

        return temporal_filtered_depth

    def _holefilling_filter(self, depth_frame):
        hole_filling = rs.hole_filling_filter()
        hole_filled_depth = hole_filling.process(depth_frame)

        return hole_filled_depth
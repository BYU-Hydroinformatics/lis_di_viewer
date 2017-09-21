from tethys_sdk.base import TethysAppBase, url_map_maker


class LisDiViewer(TethysAppBase):
    """
    Tethys app class for HKH Drough Index Viewer.
    """

    name = 'HKH Drought Index Viewer Alpha'
    index = 'lis_di_viewer:home'
    icon = 'lis_di_viewer/images/logo.png'
    package = 'lis_di_viewer'
    root_url = 'lis-di-viewer'
    color = '#2c3e50'
    description = 'View Drought Indices from LIS Model output'
    tags = 'Hydrology,SERVIR'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='lis-di-viewer',
                controller='lis_di_viewer.controllers.home'
            ),
        )

        return url_maps

@action(detail=False, methods=['get'], url_path='slider')
def slider(self, request):
    try:
        slider_items = list(
            SliderItem.objects.filter(is_active=True).order_by('order')
        )

        if not slider_items:
            return Response(
                {"error": "Slider items not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        slides = [
            {
                'id': item.id,
                'image': item.image_desktop_url,
                'imageTablet': item.image_tablet_url,
                'imageMobile': item.image_mobile_url,
                'alt': item.alt
            }
            for item in slider_items
        ]

        return Response(slides)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

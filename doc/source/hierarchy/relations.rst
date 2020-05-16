====================
API - RELATION
====================

class UML

.. uml::

    @startuml

    package api {

        package	mixins {

            package font {

                package model {

                    class FontModelMixin {
                        + draw_text()
                    }
                }

                package name {
                    class FontProportionalSpacingMixin
                    class FontMonoSpacingMixin
                    class FontNameListMixin

                    FontNameListMixin --|> FontProportionalSpacingMixin
                    FontNameListMixin --|> FontMonoSpacingMixin
                }
            }
        }

        package generics {
            class RGBColor
            class GameView
            class KeyboardController
        }

        package utils {
            class MetaMemberControl
            class SafeMember
            class ABCSafeMember
            class ShowTestDescription
            class WindowHelper
        }
    }
    @enduml

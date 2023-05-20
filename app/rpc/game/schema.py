#
# class SocketSession(BaseModel):
#     __self__: Optional[PhoneNumber] = Field(default=None)
#
#     def update_session(
#         self: "SocketSession", updated_session: Session
#     ) -> "SocketSession":
#         for session in self:
#             session[1].update(updated_session.dict())
#         return self

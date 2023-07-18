import { Avatar, List } from "antd";
import React from "react";
const data = [
  {
    title: "Ant Design Title 1",
  },
  {
    title: "Ant Design Title 2",
  },
  {
    title: "Ant Design Title 3",
  },
  {
    title: "Ant Design Title 4",
  },
  {
    title: "Ant Design Title 5",
  },
  {
    title: "Ant Design Title 6",
  },
  {
    title: "Ant Design Title 7",
  },
];
const BallotDetail = () => (
  /*
  [{position,[{candidate, votes, percent}]}]  
  */
  <List
    itemLayout="horizontal"
    dataSource={data}
    renderItem={(item, index) => (
      <List.Item>
        <List.Item.Meta
          avatar={
            <Avatar
              src={`https://xsgames.co/randomusers/avatar.php?g=pixel&key=${index}`}
            />
          }
          title={<a href="https://ant.design">{item.title}</a>}
          description="Ant Design, a design language for background applications, is refined by Ant UED Team"
        />
      </List.Item>
    )}
  />
);
export default BallotDetail;
